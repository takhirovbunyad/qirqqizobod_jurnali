from django.shortcuts import render, get_object_or_404, redirect
from django.utils.text import slugify
from django.views.generic import ListView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .forms import CommentForm, DashForm, MaqolaForm
from .models import Dash, Maqola

# -----------------------------
# Landing page
# -----------------------------
def home(request):
    return render(request, 'landing_page.html')


# -----------------------------
# Dash list view
# -----------------------------
class DashListView(ListView):
    model = Dash
    template_name = 'first_page/dash_list.html'
    context_object_name = 'dash'
    paginate_by = 12

    def get_queryset(self):
        return Dash.objects.filter(status='published').order_by('-publish')


# -----------------------------
# Maqola list view
# -----------------------------
class MaqolaListView(ListView):
    model = Maqola
    template_name = 'thirst_page/maqola_list.html'
    context_object_name = 'maqola'
    paginate_by = 12

    def get_queryset(self):
        return Maqola.objects.filter(status='published').order_by('-publish')


# -----------------------------
# Dash create view
# -----------------------------
def dash_create(request):
    if request.method == 'POST':
        form = DashForm(request.POST, request.FILES)
        if form.is_valid():
            new_dash = form.save(commit=False)
            new_dash.author = request.user
            new_dash.status = 'draft'
            new_dash.save()
            return redirect('jurnal_app:dash_list')
    else:
        form = DashForm()

    return render(request, 'first_page/dash_create.html', {'form': form})


# -----------------------------
# Maqola create view
# -----------------------------

def maqola_create(request):
    if request.method == 'POST':
        form = MaqolaForm(request.POST, request.FILES)
        if form.is_valid():
            new_maqola = form.save(commit=False)
            new_maqola.author = request.user
            new_maqola.slug = slugify(new_maqola.title)
            new_maqola.status = 'draft'
            new_maqola.save()
            return redirect('jurnal_app:maqola_list')

    else:
        form = MaqolaForm()

    return render(request, 'thirst_page/maqola_create.html', {'form': form})


# -----------------------------
# Dash detail view
# -----------------------------
def dash_detail(request, year, month, day, slug):
    dash = get_object_or_404(
        Dash,
        status='published',
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )

    comments_list = dash.comments.filter(active=True).order_by('-created')
    paginator = Paginator(comments_list, 3)  # sahifada 3 ta komment
    page_number = request.GET.get('page', 1)

    try:
        comments = paginator.page(page_number)
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.dash = dash
            new_comment.save()
            return redirect(request.path_info + f"?page={paginator.num_pages}")
    else:
        comment_form = CommentForm()

    return render(request, 'first_page/dash_detail.html', {
        'dash': dash,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
    })


from django.views.generic import DetailView


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import MaqolaCommentForm

from django.views.generic import DetailView
from django.shortcuts import redirect
from .forms import MaqolaCommentForm
from .models import Maqola

class MaqolaDetailView(DetailView):
    model = Maqola
    template_name = 'thirst_page/maqola_detail.html'
    context_object_name = 'maqola'

    def get_queryset(self):
        return Maqola.objects.filter(status='published')

    def get_object(self, queryset=None):
        return Maqola.objects.get(
            slug=self.kwargs['slug'],
            publish__year=self.kwargs['year'],
            publish__month=self.kwargs['month'],
            publish__day=self.kwargs['day'],
            status='published'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        maqola = self.get_object()
        file_type = None
        if maqola.file:
            ext = maqola.file.url.split('.')[-1].lower()
            if ext == 'pdf':
                file_type = 'pdf'
            elif ext in ['doc', 'docx']:
                file_type = 'doc'
            elif ext in ['ppt', 'pptx']:
                file_type = 'ppt'
            elif ext in ['png', 'jpg', 'jpeg']:
                file_type = 'png'
            else:
                file_type = 'other'
        context['file_type'] = file_type

        # Kommentlar
        comments_list = maqola.comments.filter(active=True).order_by('-created')
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
        paginator = Paginator(comments_list, 3)
        page_number = self.request.GET.get('page', 1)
        try:
            comments = paginator.page(page_number)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)

        context['comments'] = comments
        context['comment_form'] = MaqolaCommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = MaqolaCommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.maqola = self.object
            new_comment.save()
            return redirect(request.path_info + f"?page=1")
        context = self.get_context_data()
        context['comment_form'] = form
        return self.render_to_response(context)

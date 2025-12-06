let isCyrillic = false;

const latinToCyrillicMap = {
    'sh':'ш',
    'ch':'ч',
    'o‘':'ў',
    'g‘':'ғ',
    'a':'а','b':'б','d':'д','e':'е','f':'ф','g':'г','h':'х','i':'и','j':'ж',
    'k':'к','l':'л','m':'м','n':'н','o':'о','p':'п','q':'қ','r':'р','s':'с',
    't':'т','u':'у','v':'в','x':'х','y':'й','z':'з'
};

function toCyrillic(text) {
    let result = text;

    ['sh', 'ch', 'o‘', 'g‘'].forEach(key => {
        let regex = new RegExp(key, 'gi');
        result = result.replace(regex, function(matched){
            if (matched === matched.toUpperCase()) return latinToCyrillicMap[key].toUpperCase();
            return latinToCyrillicMap[key];
        });
    });

    for (let key in latinToCyrillicMap) {
        if (['sh','ch','o‘','g‘'].includes(key)) continue;
        let regex = new RegExp(key, 'gi');
        result = result.replace(regex, function(matched){
            if (matched === matched.toUpperCase()) return latinToCyrillicMap[key].toUpperCase();
            return latinToCyrillicMap[key];
        });
    }

    return result;
}

function convertNode(node, toCyr) {
    node.childNodes.forEach(child => {
        if (child.nodeType === Node.TEXT_NODE) {
            if (toCyr) child.textContent = toCyrillic(child.textContent);
        } else {
            convertNode(child, toCyr);
        }
    });
}

// to'g'ri komment JS da
document.getElementById('convert-btn').addEventListener('click', () => {
    const container = document.getElementById('landing-text'); // bu id HTMLdagi text id bilan mos bo'lishi kerak
    if (!isCyrillic) {
        convertNode(container, true);
        document.getElementById('convert-btn').textContent = "Lotinchaga o'tish";
        isCyrillic = true;
    } else {
        location.reload(); // oddiy reload bilan lotincha qaytarish
    }
});

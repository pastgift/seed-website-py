var prevIndex = [];
function getRandomTip() {
    var tips = [
    ]

    while (true) {
        var tipIndex = parseInt(Math.random() * tips.length + Date.now()) % tips.length;
        if (prevIndex.indexOf(tipIndex) >= 0 ) {
            continue;
        }

        prevIndex.push(tipIndex);
        if (prevIndex.length > (tips.length / 2)) {
            prevIndex.shift();
        }

        var tip = tips[tipIndex];
        return tip;
    }
}
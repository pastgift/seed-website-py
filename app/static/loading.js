function bollLoading() {
    var optBall1 = {
        direction: 1,
        rotate   : -90,
        lines    : 100,
        length   : 0,
        width    : 10,
        radius   : 10,
        corners  : 1,
        color    : '#EEDDDD',
        opacity  : 0,
        speed    : 0.35,
        trail    : 5,
        zIndex   : 2e9,
        // shadow   : true,
        hwaccel  : true,
        position : 'absolute'
    };
    var optBall2 = {
        direction: -1,
        rotate   : -90,
        lines    : 100,
        length   : 0,
        width    : 12,
        radius   : 10,
        corners  : 1,
        color    : '#DDEEDD',
        opacity  : 0,
        speed    : 0.25,
        trail    : 5,
        zIndex   : 2e9,
        // shadow   : true,
        hwaccel  : true,
        position : 'absolute'
    };
    var optBall3 = {
        direction: -1,
        rotate   : -90,
        lines    : 100,
        length   : 0,
        width    : 8,
        radius   : 10,
        corners  : 1,
        color    : '#DDDDEE',
        opacity  : 0,
        speed    : 0.5,
        trail    : 5,
        zIndex   : 2e9,
        // shadow   : true,
        hwaccel  : true,
        position : 'absolute'
    };

    new Spinner(optBall1).spin($('#spinJsTarget')[0]);
    new Spinner(optBall2).spin($('#spinJsTarget')[0]);
    new Spinner(optBall3).spin($('#spinJsTarget')[0]);
}

function clockLoading() {
    var optClockSecond = {
        direction: 1,
        rotate   : -90,
        lines    : 36,
        length   : 0,
        width    : 10,
        radius   : 115,
        corners  : 0.7,
        color    : '#FFF',
        opacity  : 0.2,
        speed    : 0.24,
        trail    : 15,
        zIndex   : 2e9,
        shadow   : true,
        hwaccel  : true,
        position : 'absolute'
    };
    var optClockMinute = {
        direction: 1,
        rotate   : -90,
        lines    : 12,
        length   : 20,
        width    : 8,
        radius   : 82,
        corners  : 1,
        color    : '#FFF',
        opacity  : 0.2,
        speed    : 0.02,
        trail    : 15,
        zIndex   : 2e9,
        shadow   : true,
        hwaccel  : true,
        position : 'absolute'
    };
    new Spinner(optClockSecond).spin($('#spinJsTarget')[0]);
    new Spinner(optClockMinute).spin($('#spinJsTarget')[0]);
}

function rollLoading() {
    var opt = {
        direction: 1,
        rotate   : -90,
        lines    : 500,
        length   : 0,
        width    : 10,
        radius   : 50,
        corners  : 1,
        color    : '#FFF',
        opacity  : 0,
        speed    : 0.24,
        trail    : 90,
        zIndex   : 2e9,
        // shadow   : true,
        hwaccel  : true,
        position : 'absolute'
    };
    new Spinner(opt).spin($('#spinJsTarget')[0]);
}
'use strict'

/***** General *****/
function strFormat() {
    var inputedArges = Array.prototype.slice.call(arguments);
    var target = inputedArges[0];
    var args   = inputedArges.slice(1);
    return target.replace(/\{(\d+)\}/g, function(m, i) {
        return args[i]
    });
}

function clearInputBox() {
    var ids = Array.prototype.slice.call(arguments);
    for (var i = 0; i < ids.length; i++) {
        $('#' + ids[i]).val('');
    }
}

function ajaxGetJson(url, successCallback, failCallback) {
    if (!successCallback) {
        successCallback = function(){};
    }

    if (!failCallback) {
        failCallback = function(){};
    }

    $.ajax({
        type       : 'GET',
        url        : url,
        dataType   : 'json',
        success    : successCallback,
        error      : failCallback
    });
}

function ajaxPostJson(url, body, successCallback, failCallback) {
    if (!successCallback) {
        successCallback = function(){};
    }

    if (!failCallback) {
        failCallback = function(){};
    }

    $.ajax({
        type       : 'POST',
        url        : url,
        data       : JSON.stringify(body),
        dataType   : 'json',
        contentType: 'application/json',
        success    : successCallback,
        error      : failCallback
    });
}

/***** Quick Filter *****/
var defaultFilterInputId = '_qfInput';
var defaultCountInputId  = '_qfCount';
var defaultTableDataId   = '_qfTableData';
var quickFilterTimer = null;

function quickFilterClearInputBox(customFilterInputId) {
    var filterInputId = defaultFilterInputId;

    if (customFilterInputId && customFilterInputId.length != 0) {
        filterInputId = customFilterInputId;
    }

    clearInputBox(filterInputId);

    $('#' + filterInputId).focus();
}

function quickFilterTableData(cookieKey, customFilterInputId, customTableDataId, customCountInputId) {
    var filterInputId = defaultFilterInputId;
    var tableDataId   = defaultTableDataId;
    var countInputId = defaultCountInputId;

    if (customFilterInputId && customFilterInputId.length != 0) {
        filterInputId = customFilterInputId;
    }

    if (customTableDataId && customTableDataId.length != 0) {
        tableDataId = customTableDataId;
    }

    if (customCountInputId && customCountInputId.length != 0) {
        countInputId = customCountInputId;
    }

    if (quickFilterTimer) {
        clearTimeout(quickFilterTimer);
    }

    quickFilterTimer = setTimeout(function() {
        var keyword = $('#' + filterInputId).val().toLowerCase();
        var rows = $('#' + tableDataId + ' > tr');
        for (var i = 0; i < rows.length; i++) {
            var targetStr = rows[i].innerText.toLowerCase().replace(/\s+/g, ' ');
            if (targetStr.indexOf(keyword) == -1) {
                $(rows[i]).hide();
            } else {
                $(rows[i]).show();
            }
        }

        if (cookieKey) {
            $.cookie(cookieKey, keyword);
        }

        quickFilterSetTableDataCount(tableDataId, countInputId);

    }, 200);
}

function quickFilterSetTableDataCount(customTableDataId, customCountInputId) {
    var tableDataId = defaultTableDataId;
    var countInputId = defaultCountInputId;

    if (customTableDataId && customTableDataId.length != 0) {
        tableDataId = customTableDataId;
    }

    if (customCountInputId && customCountInputId.length != 0) {
        countInputId = customCountInputId;
    }

    var totalRowCount = $('#' + tableDataId + ' > tr').length;
    var hiddenRowCount = $('#' + tableDataId + ' > tr:hidden').length;
    var showRowCount = totalRowCount - hiddenRowCount;
    if ($('#' + countInputId)) {
        $('#' + countInputId).val(showRowCount + ' / ' + totalRowCount);
        $('#' + countInputId).text(showRowCount + ' / ' + totalRowCount);
    }
}

function quickFilterRestoreTableDataFilter(cookieKey, customFilterInputId, customTableDataId, customCountInputId) {
    var filterInputId = defaultFilterInputId;
    var tableDataId = defaultTableDataId;
    var countInputId = defaultCountInputId;

    if (customFilterInputId && customFilterInputId.length != 0) {
        filterInputId = customFilterInputId;
    }

    if (customTableDataId && customTableDataId.length != 0) {
        tableDataId = customTableDataId;
    }

    if (customCountInputId && customCountInputId.length != 0) {
        countInputId = customCountInputId;
    }

    var keyword = $.cookie(cookieKey);
    if (keyword) {
        $('#' + filterInputId).val(keyword);
        quickFilterTableData(cookieKey, filterInputId, tableDataId, countInputId);
    }
}

function setQuickFilter(keyword, customFilterInputId) {
    var filterInputId = defaultFilterInputId;

    if (customFilterInputId && customFilterInputId.length != 0) {
        filterInputId = customFilterInputId;
    }

    $('#' + filterInputId).val(keyword);
    $('#' + filterInputId).trigger('onkeyup');
    $('#' + filterInputId).focus();
}

/***** Loading Mask *****/
var tipsTimer            = null;
var showLoadingMaskTimer = null;
var showTipsTimer        = null;
function showLoadingMask(callback) {
    if (typeof(callback) != 'function') {
        callback = function() {};
    }
    showLoadingMaskTimer = setTimeout(function() {
        $('#loadingMask').fadeIn('slow', function(){
            $('#loadingMaskContent').fadeIn('fast', callback);
            $('.container').addClass('blur');
            $('[front-content]').addClass('blur');
        });

        // 滚动提示
        setTimeout(function(){
            var nextTip = getRandomTip();
            $('#loadingTip').text(nextTip);
            $('#loadingTipSmall').text(nextTip);
            $('#loadingMaskContent').find('.loading-tip').fadeIn('slow');

            if (tipsTimer) {
                clearInterval(tipsTimer);
            }
            tipsTimer = setInterval(function(){
                $('#loadingMaskContent').find('.loading-tip').fadeOut('slow', function() {
                    var nextTip = getRandomTip();
                    $('#loadingTip').text(nextTip);
                    $('#loadingTipSmall').text(nextTip);
                    $('#loadingMaskContent').find('.loading-tip').fadeIn('slow');
                });
            }, 5000);
        }, 1000);
    }, 500);
}

function hideLoadingMask(callback) {
    if (typeof(callback) != 'function') {
        callback = function() {};
    }

    if (showLoadingMaskTimer) {
        clearTimeout(showLoadingMaskTimer);
    }

    if (showTipsTimer) {
        clearTimeout(showTipsTimer);
    }

    $('#loadingMaskContent').stop();
    $('#loadingMaskContent').fadeOut('slow', function(){
        $('#loadingMask').stop();
        $('#loadingMask').fadeOut('fast', callback);
        $('.container').removeClass('blur');
        $('[front-content]').removeClass('blur');
    });
}
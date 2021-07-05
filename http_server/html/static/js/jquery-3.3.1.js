$(document).ready(function () {
    initUi();
});
function initUi() {
    $('.header-list li').mousemove(function () {
        $(this).addClass('active');
        $(this).siblings('li').removeClass('active');
        var that = $(this).parent().parent().siblings('.inputBox').children();
        if($(this).text() == '搜索'){
            console.log('搜索!!!')
            that.removeClass('input-hiden')
        }else {
            that.addClass('input-hiden');
            that.val('')
        }
    })
}
/*
 * Main Javascript library for _noname
 * noname.trigger : used to trigger the lists
 */
noname = new Object();
noname['trigger'] = {
    click : function () {
        var isShown = true;
        var main_name = $(this).attr('id').substr(5 );
        var inner_name = main_name + '_inner';
        var content = $('#' + main_name + '_inner');
        if (content.css('display') == 'none') {
            var isShown = false;
        }
        if (content.css('display') == 'none') {
            var isShown = false;
        }
        content.slideToggle("slow");
        if (isShown) {
            $(this).text("[+] " + main_name);
        } else {
            $(this).text("[-] " + main_name);
        }
    },
}



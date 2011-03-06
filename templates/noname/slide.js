var {{ trigger }}isshown = false;
$("#{{ trigger }}").click(function(){
$("#{{ foldable }}").slideToggle("slow");
if ({{ trigger }}isshown) {
    $("#{{ trigger }}").text("[+] {{ title }}");
    {{ trigger }}isshown = false;
} else {
    $("#{{ trigger }}").text("[-] {{ title }}");
    {{ trigger }}isshown = true;
}
});

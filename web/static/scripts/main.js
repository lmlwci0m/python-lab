/*
 * li with content string creation
 */
function getListElement(content) {
    return "<li>" + content + "</li>";
}

/*
 * li iteration string creation with common prefix and postfix for content
 */
function getListElementIteration(num, basecontentprefix, basecontentpostfix) {
    retval = "";
    for (i = 0; i < num; i++) {
        retval += getListElement(basecontentprefix + " " + i + ": " + basecontentpostfix) + "\n";
    }
    return retval;
}

function getUnorderedListIteration(num, basecontentprefix, basecontentpostfix) {
    return "<ul>\n" + getListElementIteration(num, basecontentprefix, basecontentpostfix) + "</ul>\n";
}

/*
 * Shows a div blocking avery operation
 */
function showCurtain() {
    $("body").append("<div class=\"curtain\"></div>");
    $(".curtain").fadeIn(400);
}

/*
 * Removes the blocking dirs
 */
function hideCurtain() {
    $(".curtain").fadeOut(400, function(){
        $(".curtain").remove();
    });
}

function showContent(e){
    e.preventDefault();

    showCurtain();

    console.log($(this).html());

    /*
     * Get content from list element and generate a paragraph
     */
    content = $(this).html();
    content = "<p>" + content + "</p>";
    content = $("#" + $(this).attr("class")).html();

    $("section.content").delay(1000);
    console.log("after delay");
    $("section.content").queue(function(){
        $("section.content").html(content);
        console.log($(this).html());
        hideCurtain();
        $( this ).dequeue();
    });

    e.stopPropagation();

}

function hoverListElementIn(e) {
    e.preventDefault();
    $(this).animate({"background-color":"blue", "color":"white"}, 200);
}

function hoverListElementOut(e) {
    e.preventDefault();
    $(this).animate({"background-color":"white", "color":"blue"}, 50);
    if ($(this).data("sliding") == null) {
        $(this).finish();
    }
}

function showSublist(e) {
    e.preventDefault();

    $(this).data("sliding", true);
    if ($(this).data("sub") == null) {
        $(this).data("sub", true);
        sublist = "<ul class=\"sublist\"><li class=\"o1\">Option 1</li><li class=\"o2\">Option 2</li><li class=\"o3\">Option 3</li><li class=\"o4\">Option 4</li></ul>";
        $(this).append(sublist);
        $(this).animate({"height":"130px"}, 400, function(){
            if ($(this).find(".sublist").length == 0) {
                $(this).append(sublist);
            }
            $(this).find(".sublist li").click(showContent);
            $(this).data("sliding", null);
        });
    } else {
        $(this).data("sub", null);
        $(this).animate({"height":"40px"}, 400, function(){
            $(this).find(".sublist").remove();
            $(this).data("sliding", null);
        });
    }
}

var baseMain;

$(document).ready(function(){

    baseMain = $("#base-main");
    baseMainTagName = baseMain.prop("tagName");
    baseMainTagNameLower = baseMainTagName.toLowerCase();

    console.log(baseMainTagNameLower);

    /*
     * Putting mock list to nav.scrollableList
     */
    $("nav.scrollableList").html(getUnorderedListIteration(20, "Voce", "bla bla fdsif h h fajsdh jka hdsalkh ljdkshf jsdkh aflksdj hf kjashflh ashfbla bla bla bla bla bla"));

    /*
     * Handler for list selection
     */
    $("nav.scrollableList > ul > li").click(showSublist);

    /*
     * Handler for list element hover
     */
    $("nav.scrollableList ul li").hover(hoverListElementIn, hoverListElementOut);

});
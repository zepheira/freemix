(function($)
{

$.fn.qtip.styles['defaults'].background=undefined;
$.fn.qtip.styles['defaults'].color=undefined;
$.fn.qtip.styles['defaults'].tip.background=undefined;
$.fn.qtip.styles['defaults'].title.background=undefined;
$.fn.qtip.styles['defaults'].title.fontWeight = undefined;

$.fn.qtip.styles.themeroller = {
       tip: {
           corner: true                      
       },
       border: {
           width: 5,
           radius: 3
       },
       classes: {
           tooltip: 'freemix-themeable',
           tip: 'ui-widget',
           title: 'ui-widget-header',
           content: 'ui-widget-content'
       },
       width: {
           min:"300",
           max:"1000"
       }
   };
   
   })(jQuery);
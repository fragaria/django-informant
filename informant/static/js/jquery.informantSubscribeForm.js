$.fn.informantSubscribeForm = function (options) {
    var settings = $.extend({
        renderResults: false,
        resultContainer: null,
        validate: function (form, evt) { return true; }
    }, options);
    
    this.each(function () {
        var self = $(this);
        
        function renderResults(htmlContent) {
            if (settings.renderResults) {
                settings.resultContainer.html(htmlContent);
            }
        };
        
        self.submit(function (evt) {
            if (settings.validate($(this), evt)) {
                evt.preventDefault();
                
                $.post($(this).attr('action'), $(this).serialize(), function () {}, 'html')
                    .success(function (response) {
                        renderResults(response);
                        self.trigger('informantSubscribeOk', response.responseText);
                    })
                    .error(function (response) {
                        if (response.status != 400)
                            renderResults(response.statusText);
                        else
                            renderResults(response.responseText);
                        
                        self.trigger('informantSubscribeError', response.responseText);
                    });
            }
            
            return false;
        });
    });
};
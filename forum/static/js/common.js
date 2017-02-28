window.MaximumErrorCount = 5;

window.onerror = function(errorMsg, file, lineNumber) {
    window.errorCount || (window.errorCount = 0);

    if (window.errorCount <= window.MaximumErrorCount) {
        jQuery.post("{{ url_for('js_log') }}", {
            errorMessage: errorMsg,
            file: file,
            url: window.location.href,
            lineNumber: lineNumber,
            ua: navigator.userAgent
        });
    }
}

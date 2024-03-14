<script>
MathJax = {
  loader: {load: ['input/asciimath', 'output/chtml', 'ui/menu']},
  // UI/menu allows users to interact with mathjax syntax through right-click
  asciimath: {
    delimiters: [['\`','\`']],
    skipTags: ['script', 'noscript', 'style', 'textarea', 'pre'] // don't process these tags
  }

};
registerCallback('mock_exam', function() {
    MathJax.typeset();
});
</script>
<script type="text/javascript" id="MathJax-script" async
  src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/startup.js">
</script>


# Your Mock Exam Is Ready

{ mock_exam }

{ mock_exam_link }
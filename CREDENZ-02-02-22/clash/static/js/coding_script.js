document.getElementById("cfile").addEventListener("change", function () {
  var fr = new FileReader();
  fr.onload = function () {
    //   document.getElementById('editor').textContent=fr.result;
    editor.setValue(fr.result);
    //   alert(fr.result);
  };

  fr.readAsText(this.files[0]);
});


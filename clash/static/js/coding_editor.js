// const resetCodeBtn = document.querySelector('.editor__reset');

// var editor = ace.edit("editor");

ace.require("ace/ext/language_tools");
var editor = ace.edit("editor", {
  wrap: true,
});
editor.setOptions({
  enableBasicAutocompletion: true,
  enableLiveAutocompletion: true,
});

// editor.setTheme("ace/theme/monokai");
editor.setTheme("ace/theme/dracula");
editor.session.setMode("ace/mode/c_cpp");
editor.resize();
editor.setOption("showPrintMargin", false);

// $("#myModal").on("shown.bs.modal", function () {
//   $("#myInput").trigger("focus");
// });

function darkmode() {
  //   editor.setTheme("ace/theme/monokai");
  editor.setTheme("ace/theme/dracula");
  document.getElementById("lightmodebtn").style.display = "inline-block";
  document.getElementById("darkmodebtn").style.display = "none";
}

function lightmode() {
  editor.setTheme("ace/theme/xcode");
  document.getElementById("darkmodebtn").style.display = "inline-block";
  document.getElementById("lightmodebtn").style.display = "none";
}

function cleareditor() {
  // document.getElementById("editor").innerHTML = "he";
  // editor.setValue("/*your code goes here*/");
  let a = document.getElementById("textformat").value;
  if (a == "py") {
    editor.setValue("#your code goes here");
  } else {
    editor.setValue("/*your code goes here*/");
  }
}

function ecxvalues(){
  let z=editor.getValue();
// console.log(z);

  // console.log(z);
  document.getElementById("w3revi").textContent=z;
}

function fnchange() {
  var lang = document.getElementById("textformat").value;
  // alert(lang);

  if (lang == "c") {
    editor.session.setMode("ace/mode/c_cpp");
    checkcc();
    // alert("1");
  } else if (lang == "cpp") {
    editor.session.setMode("ace/mode/c_cpp");
    checkcc();
    // alert("2");
  } else if (lang == "py") {
    editor.session.setMode("ace/mode/python");
    checkcc();
    // alert("3");
  }

}

function runFunction() {
  var img = document.getElementById("uploadedImage");
  if (img.src) {
    var data = img.src.replace(/^data:image\/\w+;base64,/, "");

    // Send this data to the Flask server
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/process_image", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function () {
      if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
        console.log("Response from server: " + this.responseText);
        var tempFilePath = JSON.parse(this.responseText).tempFilePath;

        // Send the tempFilePath to the /gen_seo endpoint
        var xhr2 = new XMLHttpRequest();
        xhr2.open("POST", "/gen_seo", true);
        xhr2.setRequestHeader("Content-Type", "application/json");
        xhr2.onreadystatechange = function () {
          if (this.readyState === XMLHttpRequest.DONE && this.status === 200) {
            console.log("Response from server: " + this.responseText);
            var result = JSON.parse(this.responseText);
            document.getElementById("title").value = result.title;
            document.getElementById("desc").value = result.description;
          }
        };
        xhr2.send(JSON.stringify({ image_path: tempFilePath }));
      }
    };
    xhr.send(JSON.stringify({ image_data: data }));
  }
}

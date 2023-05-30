function uploadFile() {
  let file = document.getElementById("fileToUpload").files[0];
  let xhr = new XMLHttpRequest();
  xhr.open("POST", "/upload_endpoint", true);
  //新しいFormDataオブジェクトを作成し、ファイルに追加する
  let formData = new FormData();
  formData.append('file', file);
  //アップロードの心境状況を追跡する
  xhr.upload.addEventListener("progress", function(e) {
    let percentComplate = (e.loaded/e.total) * 100;
    document.getElementById("progress").innerText = "Progress: " + percentComplate + "%";
  });
  //エラーが発生したときに実行される関数
  xhr.addEventListener("error", function(){
    document.getElementById("message").innerText = "Error occurred during the upload.";
  });
  //アップロードが完了したときに実行される関数
  xhr.addEventListener("load", function(){
    if (xhr.status == 200) {
      document.getElementById("message").innerText = "Upload completed successfully.";
    } else {
      document.getElementById("message").innerText = "Upload failed with status" + xhr.status;
    }
  });
    xhr.send(formData);
}
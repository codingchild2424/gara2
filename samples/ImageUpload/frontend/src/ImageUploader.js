import axios from "axios";
import React, { useState } from "react";

function ImageUplodaer() {
  const [img, setImage] = useState(null);
  const [previewURL, setPreviewURL] = useState(null);

  const onChange = (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onloadend = () => {
      setImage(file);
      setPreviewURL(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const onClick = async () => {
    const formData = new FormData();
    formData.append("file", img);
    const res = await axios.post("http://localhost:5000/api/upload", formData);
    console.log(res);
  };

  return (
    <div>
      <h1>ImageUploader</h1>
      <div>
        <img
          className="profile_preview"
          src={previewURL}
          width="200px"
          heigth="200px"
        />
      </div>
      <input
        type="file"
        accept="image/jpg,image/png,image/jpeg,image/gif"
        name="image"
        onChange={onChange}
      />
      <button onClick={onClick}>업로드</button>
    </div>
  );
}

export default ImageUplodaer;

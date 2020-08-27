


function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#imageResult')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(input.files[0]);
    }
}

function store() {
    var inputClassCode = document.getElementById("classCode");
    var inputName = document.getElementById("name");


    localStorage.setItem("classCode", inputClassCode.value);
    localStorage.setItem("name", inputName.value);

    var userName = localStorage.getItem('name');
    var classCode = localStorage.getItem('classCode');

    var user = {
        "name": userName.value,
        "class_code": classCode.value

    };


    console.log(user);
    $.ajax({
        url: '/start',
        dataType: 'json',
        type: 'POST',
        data: JSON.stringify(user),
        contentType: 'application/json; charset=UTF-8',
        success: function (result) { console.log(result); }
    });
}

$(function () {
    $('#upload').on('change', function () {
        readURL(input);
    });
});

/*  ==========================================
    SHOW UPLOADED IMAGE NAME
* ========================================== */
var input = document.getElementById('upload');
var infoArea = document.getElementById('upload-label');

input.addEventListener('change', showFileName);
function showFileName(event) {
    var input = event.srcElement;
    var fileName = input.files[0].name;
    infoArea.textContent = 'File name: ' + fileName;
}





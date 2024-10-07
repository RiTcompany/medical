// class MyCustomUploadAdapter {
//     constructor(loader) {
//         this.loader = loader;
//         this.url = '/ckeditor5/image_upload/';
//     }
//
//     upload() {
//         return this.loader.file
//             .then(file => new Promise((resolve, reject) => {
//                 const formData = new FormData();
//                 formData.append('upload', file);
//
//                 fetch(this.url, {
//                     method: 'POST',
//                     body: formData,
//                     headers: {
//                         'X-CSRF-TOKEN': getCookie('csrftoken')
//                     }
//                 })
//                 .then(response => response.json())
//                 .then(data => {
//                     if (data.url) {
//                         resolve({
//                             default: data.url  // Возвращаем URL загруженного изображения
//                         });
//                     } else {
//                         reject(data.error || 'Upload failed');
//                     }
//                 })
//                 .catch(reject);
//             }));
//     }
//
//     abort() {
//         // Опционально: логика для отмены загрузки
//     }
// }
//
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function() {
    // Указываем правильный селектор для инициализации CKEditor
    let context = document.querySelector('#id_content').value;
    let context_latin = document.querySelector('#id_content_latin').value;
    ClassicEditor.create(document.querySelector('#id_content'), {
        simpleUpload: {
            uploadUrl: '/ckeditor5/image_upload/',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        },
        blockToolbar: {
                items: [
                    "paragraph",
                    "heading1",
                    "heading2",
                    "heading3",
                    "|",
                    "bulletedList",
                    "numberedList",
                    "|",
                    "blockQuote",
                ],
        },
        toolbar: {
            items: [
                "heading",
                 "codeBlock",
                 "|",
                 "insertImage",
                 "fontColor",
                 "|",
                 "bold",
                 "italic",
                 "link",
                 "underline",
                 "strikethrough",
                 "code",
                 "subscript",
                 "superscript",
                 "highlight",
                 "|",
                 "bulletedList",
                 "numberedList",
                 "todoList",
                 "|",
                 "blockQuote",
                 "outdent",
                 "indent",
                 "|",
                 "fontSize",
                 "fontFamily",
                 "fontBackgroundColor",
                 "mediaEmbed",
                 "removeFormat",
                 "insertTable",
                 "sourceEditing",
            ]
        },
        image: {
            toolbar: [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
                "toggleImageCaption",
                "|"
            ],
            styles: [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        heading: {
            options: [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h1",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
        list: {
            properties: {
                "styles": true,
                "startIndex": true,
                "reversed": true,
            }
        },
        htmlSupport: {
            allow: [
                {"name": "/.*/", "attributes": true, "classes": true, "styles": true}
            ]
        },
        fontFamily: {
            options: [
                'default',
                'Arial, Helvetica, sans-serif',
                'Courier New, Courier, monospace',
                'Georgia, serif',
                'Lucida Sans Unicode, Lucida Grande, sans-serif',
                'Tahoma, Geneva, sans-serif',
                'Times New Roman, Times, serif', // Times New Roman должен быть в списке опций
                'Trebuchet MS, Helvetica, sans-serif',
                'Verdana, Geneva, sans-serif'
            ],
            supportAllValues: true
        },
        // Устанавливаем Times New Roman через содержимое
        extraPlugins: ['Font'],
        language: 'en',
        height: 400,
        width: '100%',
        // Добавляем кастомный CSS для настройки шрифта по умолчанию
    })
    .then(editor => {
        if (!context){
            editor.setData('<span class="text-big" style="font-family: Times New Roman, Times, serif;">&shy;</span>');
        }
    })
    .catch(error => {
        console.error('Ошибка инициализации CKEditor:', error);
    });
    ClassicEditor.create(document.querySelector('#id_content_latin'), {
        simpleUpload: {
            uploadUrl: '/ckeditor5/image_upload/',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        },
        blockToolbar: {
                items: [
                    "paragraph",
                    "heading1",
                    "heading2",
                    "heading3",
                    "|",
                    "bulletedList",
                    "numberedList",
                    "|",
                    "blockQuote",
                ],
        },
        toolbar: {
            items: [
                "heading",
                 "codeBlock",
                 "|",
                 "insertImage",
                 "fontColor",
                 "|",
                 "bold",
                 "italic",
                 "link",
                 "underline",
                 "strikethrough",
                 "code",
                 "subscript",
                 "superscript",
                 "highlight",
                 "|",
                 "bulletedList",
                 "numberedList",
                 "todoList",
                 "|",
                 "blockQuote",
                 "outdent",
                 "indent",
                 "|",
                 "fontSize",
                 "fontFamily",
                 "fontBackgroundColor",
                 "mediaEmbed",
                 "removeFormat",
                 "insertTable",
                 "sourceEditing",
            ]
        },
        image: {
            toolbar: [
                "imageTextAlternative",
                "|",
                "imageStyle:alignLeft",
                "imageStyle:alignRight",
                "imageStyle:alignCenter",
                "imageStyle:side",
                "|",
                "toggleImageCaption",
                "|"
            ],
            styles: [
                "full",
                "side",
                "alignLeft",
                "alignRight",
                "alignCenter",
            ],
        },
        heading: {
            options: [
                {
                    "model": "paragraph",
                    "title": "Paragraph",
                    "class": "ck-heading_paragraph",
                },
                {
                    "model": "heading1",
                    "view": "h1",
                    "title": "Heading 1",
                    "class": "ck-heading_heading1",
                },
                {
                    "model": "heading2",
                    "view": "h2",
                    "title": "Heading 2",
                    "class": "ck-heading_heading2",
                },
                {
                    "model": "heading3",
                    "view": "h1",
                    "title": "Heading 3",
                    "class": "ck-heading_heading3",
                },
            ]
        },
        list: {
            properties: {
                "styles": true,
                "startIndex": true,
                "reversed": true,
            }
        },
        htmlSupport: {
            allow: [
                {"name": "/.*/", "attributes": true, "classes": true, "styles": true}
            ]
        },
        fontFamily: {
            options: [
                'default',
                'Arial, Helvetica, sans-serif',
                'Courier New, Courier, monospace',
                'Georgia, serif',
                'Lucida Sans Unicode, Lucida Grande, sans-serif',
                'Tahoma, Geneva, sans-serif',
                'Times New Roman, Times, serif', // Times New Roman должен быть в списке опций
                'Trebuchet MS, Helvetica, sans-serif',
                'Verdana, Geneva, sans-serif'
            ],
            supportAllValues: true
        },
        language: 'en', // Устанавливаем язык редактора
    })
    .then( editor => {
        if (!context_latin){
        editor.setData('<span class="text-big" style="font-family: Times New Roman, Times, serif;">&shy;</span>');
    }
    } )
    .catch(error => {
        console.error('Ошибка инициализации CKEditor:', error);
    });
    let content = document.querySelectorAll(".ck.ck-reset.ck-editor.ck-rounded-corners");
    content[0].style.display = "none";
    content[1].style.display = "none";
});



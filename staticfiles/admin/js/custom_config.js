document.addEventListener("DOMContentLoaded", function() {
    // Указываем правильный селектор для инициализации CKEditor
    let context = document.querySelector('#id_content').value;
    let context_latin = document.querySelector('#id_content_latin').value;
    ClassicEditor.create(document.querySelector('#id_content'), {
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
        contentsCss: [
            'https://cdn.ckeditor.com/ckeditor5/34.1.0/classic/theme.css', // Основные стили CKEditor
            '{% static "css/custom_ckeditor.css" %}' // Ваши кастомные стили
        ]
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
                'Times New Roman, Times, serif', // Times New Roman по умолчанию
            ],
            supportAllValues: true
        },
        font_defaultLabel: 'Times New Roman',
        fontSize_defaultLabel: 'Big',
        language: 'en', // Устанавливаем язык редактора
        contentsCss: [
            'http://cdn.ckeditor.com/4.25.0-lts/full-all/contents.css',
            'https://ckeditor.com/docs/ckeditor4/4.25.0-lts/examples/assets/css/classic.css'
        ],
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



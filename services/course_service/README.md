# Описание
Храним иерархию курс->подкурсы->пункты в которых уже либо задачи, либо видео, либо конспекты

По умолчанию курсы скрыты пока не окнет админ

# Ручки

Возвращает список видео for autors only
### post /api/v1/course  - создать курс 
`{
    parent_course_id: uuid
    content:
    {
        item_id: 
        {
            type: video|text|task
            id: uuid
        },
        item_id: 
        {
            type: video|text|task
            id: uuid
        },
        item_id: 
        {
            type: video|text|task
            id: uuid
        },
    }
}`
return id

### put /internal/update/course/{course_id}/item/{item_id}  - создать айтем курса
`{
    parent_course_id: uuid
    id: uuid
    type: video|text|task 
}`


### delete /api/v1/course/{id}
delete course by id

### get /api/v1/course/{id}
Подумать, возможно стоит сразу возвращать агрегат.
return custom course by id
`{
    parent_course_id: uuid
    author: uuid
    content:
    {
        item_id: 
        {
            type: video|text|task
            id: uuid
        },
        item_id: 
        {
            type: video|text|task
            id: uuid
        },
        item_id: 
        {
            type: video|text|task
            id: uuid
        },
    }
    child_course_ids:[
        uud1,
        uud2...
    ]
}`

### get /api/v1/courses - retrun list of courses by filter
params:
    active: [True, False]. False for admin users only

### post /api/v1/admin/course/{id}/activate
Activate course - admin only

### post /api/v1/admin/course/{id}/deactivate
Deactivate course - admin only

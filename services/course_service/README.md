# Описание
Храним иерархию курс->подкурсы->пункты в которых уже либо задачи, либо видео, либо конспекты

По умолчанию курсы скрыты пока не окнет админ

# Ручки

### post /course  - создать курс 
`{
    parent_course_id: uuid
    content:
    [
        loaded_video_id,
        loaded_text_id,
        loaded_video_id,
        loaded_task_id,
    ]
}`
return id

### delete /course/{id}
delete course by id

### get /course/{id}
Подумать, возможно стоит сразу возвращать агрегат.
return custom course by id
`{
    parent_course_id: uuid
    author: uuid
    content:
    [
        loaded_video_id,
        loaded_text_id,
        loaded_video_id,
        loaded_task_id,
    ]
    child_course_ids:[
        uud1,
        uud2...
    ]
}`

### get /courses - retrun list of courses by filter
params:
    active: [True, False]. False for admin users only
    page: Page

### post /course/{id}/activate
Activate course - admin only

### post /couse/{id}/deactivate
Deactivate course - admin only

### post /couse/{id}/complete/{item_id}
Deactivate course - admin only
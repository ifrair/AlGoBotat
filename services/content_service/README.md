# Описание
Храним видео и конспекты

Для стриминга видео можно использовать Objective storage

Objective storage

# Ручки

### post /api/v1/video
Cоздает и возвращает id видео
`
{
    course_id: uuid
    item_id: int
    file: file
}
`
return id

### delete /api/v1/video/{id}
delete video - for author only and admins only


### get /api/v1/video/{id}
Возвращает видео по id
`{  
    status: loaded 
    video_link: str?
}`
return id

### post /api/v1/text
create text
`{
    course_id: uuid
    item_id: int
    content: content
}`
return id

### put /api/v1/text
Изменяет задачку по task_id
`
{
    task_id: uuid
    content: text
}
`

### delete /api/v1/text/{id} 
delete text by id, for authors and admins only.

### get /api/v1/text/{id}
`{
    status: loaded
    content: str?
}`
Возвращает текст по id

### post /api/v1/task
Cоздает и возвращает задачку 
`
{
    course_id: uuid
    item_id: int
    content: text
}
`


### put /api/v1/task
Изменяет задачку по id
`
{
    task_id: uuid
    content: text
}
`

### get /api/v1/task/{id}
Возвращает задачку
`
{
    status: loaded
    file: file?
}
`
### delete /api/v1/task/{id}
delete task by id, for authors and admins only. 



# Описание
Храним видео и конспекты

Для стриминга видео можно использовать Objective storage

Objective storage
# Ручки

### post /video
Cоздает и возвращает id видео
`
{
    file: file
}
`
### delete /video/{id}
delete video - for author and admins only

### get /video/{id}
Возвращает видео по id

### get /videos
params:
    * page_id

Возвращает список видео

### post /text
create text
`{
    content: content
}`

### delete /text/{id} 
delete text by id, for auhot and admins only.

### get /text/{id}

Возвращает текст по id

### get /texts
params:
* page
* author
* completed

Возвращаем список текстов

### post /task
Cоздает и возвращает задачку 
`
{
    content: text
}
`
### get /task/{id}
Возвращаем задачку
`
{
    file: file
}
`
### delete /task/{id}
delete task by id, for authors and admins only.
 
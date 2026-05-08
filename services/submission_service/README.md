Тестируем посылки, везде можно сделать ограничение 1 сек + 256 мб. 

Храним посылки и актуальные статусы тестирования

Посылок будет много так что обдумываем бд тщательно

Поддерживаем как можно больше языков. Как минимум js, java, python, c, c++, c#, go

# Ручки

### post /api/v1/submit
`{
    content: text
    language: js, java, python, c, c++, c#, go, typescipt, ruby, rust 
    item_id: uuid
    course_assigment_id: uuid

}`


### get /api/v1/submit/{id}
get submition by id
`{
    verdict: "OK"
    logs: text
    status: processing | completed
    time: 50 #ms 
    memory: 128
    language: js, java, python, c, c++, c#, go, typescipt, ruby, rust 
    content: text
    item_id: uuid
    course_assigment_id: uuid
    created_date: date
    updated_date
}`





### get /api/v1/submits
    params: 
        * task_id
    description:
        for a user return his submissions 

### get /api/v1/admin/submits
    params: 
        * task_id
    description:
        for user returns all submissions

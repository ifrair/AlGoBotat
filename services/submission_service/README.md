Тестируем посылки, везде можно сделать ограничение 1 сек + 256 мб. 

Храним посылки и актуальные статусы тестирования

Посылок будет много так что обдумываем бд тщательно

Поддерживаем как можно больше языков. Как минимум js, java, python, c, c++, c#, go

# Ручки

### post /submit
`{
    content: text
    language: js, java, python, c, c++, c#, go, typescipt, ruby, rust 
    task_id: uuid
}`


### get /submit/{id}
get submition by id
`{
    verdict: "OK"
    logs: text
    time: 50 #ms 
    memory: 128
    language: js, java, python, c, c++, c#, go, typescipt, ruby, rust 
    content: text
    task_id: uuid
}`



### get /submits
    params: 
        page
        task_id
    description:
        for a user return his submissions 
        for admins returns all submissions

### delete /submit/{id}
    remove submit
    for admins user only


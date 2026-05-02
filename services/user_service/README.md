
По ощущениям самый простой сервис, управление бд пользователей.

Ответственность: данные юзера и граф подписок на курсы

Даем возможность управлять админу

# Ручки

### get /user/{id}
get user by id for admin

### post /user
`{
    ...
}`
create user - for admin only


### get /user/find_by_email/{enail
`{
    ...
}`

get user by email - for admin only


### get /user
list users for admin

### get /user
user info for the current user 

### post /user/{id}/ban
ban user

### post /user/{id}/unban
unban user

### delete /user/{id}
delete user
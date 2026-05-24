
По ощущениям самый простой сервис, управление бд пользователей.

Ответственность: данные юзера и граф подписок на курсы

Даем возможность управлять админу

# Ручки

### get  /api/v1/admin/user/{id}
get user by id for admin

### post /user
`{
    ...
}`
create user - for admin only


### get  /api/v1/user/admin/find_by_email/{email}
`{
    ...
}`

get user by email - for admin only


### get  /api/v1/admin/users
list users for admin

### get  /api/v1/user
user info for the current user 

### post  /api/v1/admin/user/{id}/ban
ban user

### post  /api/v1/admin/user/{id}/unban
unban user

### delete  /api/v1/admin/user/{id}
delete user

### post  /api/v1/admin/course_assigment
`{
    course_id: uuid
    user_id: uuid
}`

return {id}

### post  /api/v1/course_assigment
`{
    course_id: uuid
}`

return {id}

### get  /api/v1/course_assigment/{id}
`{
    course_id: uuid
    user_id: uuid
    status: uncompleted 
    progress_percentage: 80
    progress:
        content: {
            item_id: status
        }
        submissions:
            {
                item_id: submission_id
            }
}`
returns course assigment by id


### get  /api/v1/course_assigments
`[
{
    course_id: uuid
    user_id: uuid
    status: uncompleted 
    progress_percentage: 80
    progress:
        content: {
            item_id: status
        }
        submissions:
            {
                item_id: submission_id
            }
}
...
]`

returns course assigments for the user

### get  /api/v1/admin/course_assigments
`[
{
    course_id: uuid
    user_id: uuid
    status: uncompleted 
    progress_percentage: 80
    progress:
        content: {
            item_id: status
        }
        submissions:
            {
                item_id: submission_id
            }
}
...
]`

returns course assigments for all users for admin

### get  /api/v1/admin/course_assigments/{user_id}
`[{
    course_id: uuid
    user_id: uuid
    status: uncompleted 
    progress_percentage: 80
    progress:
        content: {
            item_id: status
        }
        task:
            {
                "last_submission_id": last_submission_id
                "submissions":
                    [
                        submission_id,
                        submission_id,
                        ...
                    ]           
            }
}
...
]`

returns course assigments for a user for admin


### post /internal/v1/course_assigments/{course_assigments_id}/content/{item_id}/status
`
[
{

    status: completed 
}
...
]`

complete course assigment for id

### post /internal/v1/course_assigments/{course_assigments_id}/task/{item_id}
`{
    "item_id": submission_id
 }
`

### post /internal/v1/course_assigments/{course_assigments_id}/status
`{
    status: completed 
 }
`
export interface Profile {
    username: string,
    snowflake: number,
    avatar_url: string,
    in_server: boolean,
    is_admin: boolean,
    is_banned: boolean,
    partner: number
}
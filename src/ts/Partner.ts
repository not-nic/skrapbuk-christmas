import {Answers} from "./Answers.ts";

export interface Partner {
    details: {
        snowflake: number,
        username: string,
        avatar_url: string
    },
    answers: Answers
}
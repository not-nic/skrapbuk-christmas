import { defineStore } from "pinia";
import axios from "axios";

interface Profile {
    username: string,
    snowflake: number,
    avatar_url: string,
    in_server: boolean,
    is_admin: boolean,
    is_banned: boolean,
    partner: number
}

export const useUserStore = defineStore('userStore', {
    state: () => ({
        user: {} as Profile,
        rotateDeg: 0,
        defaultImg: "../src/assets/gom.webp",
        clickCount: 0,
        showCopy: false,

        revealedCard: true,
        eventStarted: true
    }),

    actions: {
        /**
         * Easter egg function to spin the users avatar when clicked.
         */
        spinAvatar() {
            this.rotateDeg += 360;
            this.clickCount += 1;

            if (this.clickCount > 25) {
                this.clickCount = 0;
                this.user.avatar_url = this.defaultImg;
            }
        },

        /**
         * Asynchronous function to get an authorised users discord details from Flask.
         */
        async getUser() {
            try {
                // if authed, get the user's details and add them to the user object.
                const response = await axios.get("/api/users/me", {withCredentials: true})
                this.user = response.data;
            } catch (error: any) {

                let http_status = error.response?.status;

                // check if the user is unauthorised, if so redirect them to the login page.
                if (http_status === 401) {
                    window.location.href = "/api";
                } else if (http_status === 403) {
                    this.$router.push("banned")
                } else {
                    console.error('Non-401/403 error:', error);
                }
            }
        },

        /**
         * Allow a user to copy their own discord snowflake to clipboard.
         * @param snowflake - discord snowflake to copy.
         */
        async copySnowflake(snowflake: number) {
            try {
                await navigator.clipboard.writeText(snowflake.toString());
                console.log("Copied Snowflake");
            } catch (e) {
                console.error("Cannot copy", e)
            }
        },

        /**
         * Toggle to see if the user has revealed their partner, by saving a key/value to local storage.
         */
        revealPartner(): void {
            const hasRevealed = localStorage.getItem('revealedCard') === 'true';
            if (!hasRevealed) {
                localStorage.setItem('revealedCard', 'true');
                this.revealedCard = true;
            } else {
                this.revealedCard = false;
            }
        }
    }
})
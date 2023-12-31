import { defineStore } from "pinia";
import axios from "axios";
import {Partner} from "../ts/Partner.ts";
import {Profile} from "../ts/Profile.ts";

export const useUserStore = defineStore('userStore', {
    state: () => ({
        user: {} as Profile,
        partner: {} as Partner,

        revealedCard: false,
        showNoPartnerMessage: false,
        noPartnerMessage: "",

        selectedMenuItem: "partner"
    }),

    actions: {
        /**
         * Custom error handler for backend responses, uses a switch case on known responses such as 401 or 403.
         * @param error {any} - Axios error object
         * @param customHandlers {object} - Custom response such as an error message contents,
         * or boolean to activate a v-if.
         */
        async errorHandler(error: any,
                           customHandlers: { customErrorHandler?: (error: any) => void} = {}): Promise<void> {
            // get status code from response
            let httpStatus = error.response?.status;

            const handleDefault = () => {
                // TODO: Redirect user to an error page, on requests statuses like 500.
                console.error('Unhandled error:', error);
            };

            switch(httpStatus) {
                // if the user is unauthorised, redirect them to the login page.
                case 401:
                    window.location.href = "/api"
                    break;
                // 403 is returned from banned users, redirect them to /banned.
                case 403:
                    window.location.href= "/banned"
                    break;
                // 400 errors can require different edge cases such, i.e. an error message.
                case 400:
                    if (customHandlers.customErrorHandler) {
                        customHandlers.customErrorHandler(error)
                    }
                    break;
                case 500:
                    console.error("Uh oh!, a server error, that's no good!")
                    break;
                // if no errors are found, log the unhandled error.
                default: handleDefault();
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
            } catch (error) {
                await this.errorHandler(error)
            }
        },

        /**
         * Asynchronous function to get an authorised users partners from Flask.
         */
        async getPartner() {
            try {
                const response = await axios.get("/api/users/partner", {withCredentials: true})
                this.partner = response.data
            } catch (error: any) {
                await this.errorHandler(error, {
                    customErrorHandler: () => {
                        this.noPartnerMessage = `${error.response.data.error}`;
                        this.showNoPartnerMessage = true;
                    }
                })
            }
        },

        /**
         * Toggle to see if the user has revealed their partner, by saving a key/value to local storage.
         */
        revealPartner(): void {
            const hasRevealed: boolean = localStorage.getItem('revealedCard') === 'true';
            if (!hasRevealed) {
                localStorage.setItem('revealedCard', 'true');
                this.revealedCard = true;
            } else {
                this.revealedCard = false;
            }
        },

        /**
         * function to change the current selected menu item.
         * @param item {string} menu item to be switched to.
         */
        selectMenuItem(item: string) {
            this.selectedMenuItem = item;
        }
    }
})
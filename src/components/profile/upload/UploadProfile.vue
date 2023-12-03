<script lang="ts">
import {defineComponent} from 'vue'
import axios from "axios";
import {useUserStore} from "../../../stores/UserStore.ts";

export default defineComponent({
  name: "UploadProfile",

  data() {
    return {
      userStore: useUserStore(),
      artwork: null as File | null,

      artworkLoaded: false,
      artworkUrl: "",
      artworkErrorMessage: "",
      uploadMessage: ""
    }
  },

  methods: {
    /**
     * Get uploaded artwork from the database, and display it within the artwork preview card.
     */
    loadArtwork() {
      const endpoint = "/api/users/artwork";

      axios.get(endpoint, {withCredentials: true})
        .then(response => {
          if (response.status === 200) {
            this.artworkLoaded = true;
            this.artworkUrl = endpoint;
          } else {
            this.artworkErrorMessage = response.data.error || 'An unexpected error occurred.';
          }
        })
        .catch(error => {
          this.artworkErrorMessage = error.response.data.error || 'An unexpected error occurred.';
        })
    },

    /**
     * Handle user drag & drop operation by taking the first item and uploading that to the backend.
     * @param event - The DragEvent object.
     */
    handleDrop(event: DragEvent) {
      event.preventDefault();
      const artwork = event.dataTransfer?.files;

      if (artwork && artwork.length > 0) {
        this.artwork = artwork[0]
        this.uploadArtwork(artwork[0]);
      }
    },
    /**
     * Method to change the users selected artwork, before uploading it to the backend.
     * @param event
     */
    changeArtwork(event: Event) {
      const target = event.target as HTMLInputElement;

      if (target.files && target.files.length > 0) {
        this.artwork = target.files[0];
      } else {
        this.artwork = null;
      }
    },

    /**
     * Method to upload users artwork, returning error messages based on file format &
     * @param artwork
     */
    async uploadArtwork(artwork: File | null) {
      if (artwork) {
        try {
          const formData = new FormData();
          formData.append('image', artwork);
          const response = await axios.post("/api/users/upload", formData, {
            headers: {
              "Content-Type": "multipart/form-data",
              withCredentials: true
            }
          });

          this.uploadMessage = response.data.message;
          this.loadArtwork();
        } catch (error: any) {
          this.uploadMessage = error.response.data.error
        }
      }
    }
  },

  computed: {
    partnerUsername() {
      return this.userStore.partner.details.username
    }
  },

  mounted() {
    this.loadArtwork()
  }
})
</script>

<template>
<div class="content">
  <div class="preview-artwork">
    <div class="preview-header">
      <p>To <span class="red">{{partnerUsername}}</span></p>
    </div>
    <img v-if="artworkLoaded" :src="artworkUrl" alt="Preview artwork" />
    <p v-else>{{ artworkErrorMessage }}</p>
    <p>This is your current uploaded file for {{partnerUsername}}, make changes by uploading a new file!</p>
  </div>
  <div class="upload">
    <div
      class="drag-container"
      @dragover.prevent
      @dragenter.prevent
      @drop="handleDrop"
    >
      <div class="text">
        <div class="title">
          <h1>Drag & Drop</h1>
          <h1>Your <span class="red">Artwork</span>.</h1>
        </div>
        <p>- or -</p>
        <div class="upload-btn">
          <input type="file" @change="changeArtwork" ref="image" />
          <button :disabled="!artwork" @click="uploadArtwork(artwork)">Upload Artwork</button>
        </div>
        <p class="red" v-if="uploadMessage">{{uploadMessage}}</p>
      </div>
    </div>
  </div>
</div>
</template>

<style scoped>
.content {
  flex: 1;
  display: flex;
  flex-direction: row;
  gap: 1rem;
}

.upload {
  box-sizing: border-box;
  width: 100%;
  height: 600px;
  border-radius: 14px;
  background-color: #2c2760;
  box-shadow: 6px 6px 0 0 rgba(0, 0, 0, 0.10);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  overflow: auto;
}

.drag-container {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  border-radius: 10px;
  border: 4px dashed #FF7A6F;
  background: rgba(0, 0, 0, 0.25);
}

h1, h2 {
  color: #FFF2DB;
  margin: 0;
  font-family: 'Fredoka', sans-serif;
  letter-spacing: 0.1rem;
}

.red {
  opacity: 1;
  color: #FF7A6F;
}

p {
  opacity: 0.5;
  text-align: center;
  color: #FFF6E7;
}

.text {
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  padding: 1rem;
}

button {
  text-align: center;
  font-family: 'Fredoka', sans-serif;
  padding: 0.4em 2em;
  font-size: 1.2rem;
  letter-spacing: 0.06rem;
  border-radius: 6px;
  color: #FFF2DB;
  background-color: #544ab3;
}

button:hover:not(:disabled) {
  background-color: #7165e3;
  border-color: #0000001A;
}

button:disabled {
  background-color: #888888;
  border-color: #0000001A;
  cursor: not-allowed;
}

.upload-btn {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0.5rem;
}

.preview-artwork {
  box-sizing: border-box;
  width: 100%;
  height: 100%;
  max-width: 340px;
  min-height: 600px;
  border-radius: 14px;
  background: linear-gradient(-195deg, #2C2760 36.34%, #373268 36.34%, #373268 95.9%);
  box-shadow: 6px 6px 0 0 rgba(0, 0, 0, 0.10);
  padding: 1rem;

  display: flex;
  flex-direction: column;
  justify-content: space-around;
  gap: 1rem;
}

img {
  box-sizing: border-box;
  width: 100%;
  aspect-ratio: 1/1;
  object-fit: cover;
  border: 0.5rem solid rgb(0, 0, 0, 0.3);
  border-radius: 50%;
}

.preview-header {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.preview-header > p {
  opacity: 1;
  font-size: 1.2rem;
}

@media screen and (max-width: 600px) {
  .upload {
    height: 100%;
  }
}

@media screen and (max-width: 1000px) {
  .content {
    flex-direction: column;
  }

  .preview-artwork {
    max-width: 100%;
    min-height: 0;
  }
}

@media screen and (max-width: 1300px) {
  .upload-btn {
    flex-direction: column;
    align-items: center;
  }
}
</style>
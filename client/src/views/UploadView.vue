<script setup
        lang="ts">
        import UploadButton from "@/components/UploadButton.vue";
        import UploadLoader from "@/components/UploadLoader.vue";
        import PreviewHeader from "@/components/PreviewHeader.vue";
        import { useImageStore } from "@/stores/imageStore";
        import { postImage } from "@/api/ImageApi";
        import { ref } from "vue";
        import ModalComponent from "@/components/ModalComponent.vue";


        let file: File;
        const imageStore = useImageStore();
        const fileName = ref<string>('');
        const beingScanned = ref<boolean>(false);
        const showModal = ref<boolean>(false);
        const isDraggedOver = ref<boolean>(false);

        async function handleUpload($event: Event) {
            const inputTarget = $event.target as HTMLInputElement;
            const fileReader = new FileReader();
            if (!inputTarget.files?.[0]) return;
            file = inputTarget.files[0];
            fileReader.onload = (e) => {
                imageStore.addImage(e.target?.result as string)
            };
            await new Promise((resolve) => {
                fileReader.onloadend = () => resolve(fileReader.result);
                fileReader.readAsDataURL(file);
            });
            fileName.value = file['name'];
        }

        async function scanForm() {
            showModal.value = false;
            beingScanned.value = true;
            await postImage(file);
            showModal.value = true;
            beingScanned.value = false;
        }

</script>

<template>
    <main class="flex flex-col items-center transition-all relative h-5/6">
        <label v-if="!imageStore.uploadedImage"
               for="fileInput"
               @dragover="isDraggedOver = true;"
               @dragleave="isDraggedOver = false;"
               class="transition-color duration-150 flex flex-col items-center justify-center mt-8 px-10 max-w-[700px] w-[80svw] max-h-[500px] h-[60svh] border-dashed border-gray-500 border-2 rounded-md"
               :class="{ 'border-green-500': isDraggedOver }">
            <UploadButton @change="handleUpload" />
            <p class="mt-7">Drag and drop your .png or .jpeg image here or click to select.</p>
        </label>
        <PreviewHeader v-if="imageStore.uploadedImage"
                    :being-scanned="beingScanned"
                    @scanform="scanForm" 
                    @click="handleUpload"
                    />
        <div class="relative">
            <div v-if="beingScanned"
                 class="absolute flex items-center inset-0 bg-zinc-600/50 rounded-lg backdrop-blur-[1px]">
                <UploadLoader />
            </div>
            <img v-if="imageStore.uploadedImage"
                 class="max-h-[32rem] rounded-lg object-contain"
                 :src="imageStore.uploadedImage" />
        </div>
        <p v-if="fileName"
           class="ms-2">{{ fileName }}</p>
        <ModalComponent @close="showModal = false;"
                        :isVisible="showModal">
            <template #header>
                {{ fileName }}
            </template>
            <img v-if="imageStore.uploadedImage"
                 class="rounded-sm"
                 :src="imageStore.uploadedImage" />
            <template #footer>
                <button class="transition-colors bg-green-600 hover:bg-green-900 rounded-md mx-auto mt-2 size-10">
                    <i class="bi bi-download text-2xl"></i>
                </button>
            </template>
        </ModalComponent>
    </main>
</template>

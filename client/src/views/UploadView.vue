<script setup
        lang="ts">
        import UploadLoader from "@/components/UploadLoader.vue";
        import PreviewHeader from "@/components/PreviewHeader.vue";
        import ModalComponent from "@/components/ModalComponent.vue";
        import DragAndDrop from "@/components/DragAndDrop.vue";
        import { useImageStore } from "@/stores/imageStore";
        import { postImage } from "@/api/ImageApi";
        import { ref } from "vue";


        let file: File;
        const imageStore = useImageStore();
        const fileName = ref<string>('');
        const beingScanned = ref<boolean>(false);
        const showModal = ref<boolean>(false);
        const error = ref<string>('');

        async function handleUpload($event: Event) {
            if ($event instanceof DragEvent && $event.dataTransfer?.files[0]) {
                file = $event.dataTransfer?.files[0] as File;
            } else {
                const inputTarget = $event.target as HTMLInputElement;
                if (!inputTarget.files?.[0]) return;
                file = inputTarget.files[0];
            }
            const fileReader = new FileReader();
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
            try {
                await postImage(file);
            } catch (e: any) {
                error.value = e.message;
            }
            showModal.value = true;
            beingScanned.value = false;
        }

</script>

<template>
    <main class="flex flex-col items-center transition-all relative h-5/6">
        <DragAndDrop @drop.stop.prevent="handleUpload"
                     @change="handleUpload" />
        <PreviewHeader v-if="imageStore.uploadedImage"
                       :being-scanned="beingScanned"
                       @scanform="scanForm"
                       @click="handleUpload" />

        <div class="relative">
            <div v-if="beingScanned"
                 class="absolute flex items-center inset-0 bg-zinc-600/50 rounded-lg backdrop-blur-[1px]">
                <UploadLoader />
            </div>
            <div v-if="error"
                 class="absolute flex justify-center inset-0 bg-zinc-600/50 rounded-lg backdrop-blur-[1px]">
                <i class="bi bi-exclamation-triangle"></i>
                <p>Error: {{ error }}</p>
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
                 class="max-h-[36rem] object-contain rounded-sm"
                 :src="imageStore.uploadedImage" />
            <template #footer>
                <button class="transition-colors bg-green-600 hover:bg-green-900 rounded-md mx-auto mt-2 size-10">
                    <i class="bi bi-download text-2xl"></i>
                </button>
            </template>
        </ModalComponent>
    </main>
</template>

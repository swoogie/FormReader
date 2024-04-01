<script setup
        lang="ts">
        import UploadLoader from "@/components/UploadLoader.vue";
        import PreviewHeader from "@/components/PreviewHeader.vue";
        import ModalComponent from "@/components/ModalComponent.vue";
        import DragAndDrop from "@/components/DragAndDrop.vue";
        import { useImageStore } from "@/stores/imageStore";
        import { postImage } from "@/api/ImageApi";
        import { ref, nextTick } from "vue";
        import { jsPDF } from "jspdf";


        let resolution: { width: number, height: number };
        const imageStore = useImageStore();
        const fileName = ref<string>('');
        const beingScanned = ref<boolean>(false);
        const showModal = ref<boolean>(false);
        const error = ref<string>('');
        const checkboxCoords = ref<number[][]>();
        const inputFieldCoords = ref<number[][]>();
        const scannedImage = ref<HTMLImageElement>();
        const domToActualRatio = ref<number>();
        const form = ref<HTMLElement>();

        async function handleUpload($event: Event) {
            let file: File;
            if ($event instanceof DragEvent && $event.dataTransfer?.files[0]) {
                file = $event.dataTransfer?.files[0] as File;
            } else {
                const inputTarget = $event.target as HTMLInputElement;
                if (!inputTarget.files?.[0]) return;
                file = inputTarget.files[0];
            }
            const fileReader = new FileReader();
            fileReader.onload = async (e) => {
                const imageDataUrl = e.target?.result as string;
                imageStore.addImage(imageDataUrl, file);
                resolution = await new Promise((resolve) => {
                    const image = new Image();
                    image.src = imageDataUrl;
                    image.onload = () => {
                        resolve({ width: image.naturalWidth, height: image.naturalHeight });
                    };
                });
            };
            await new Promise<void>((resolve) => {
                error.value = '';
                fileName.value = file['name'];
                fileReader.readAsDataURL(file);
                fileReader.onloadend = () => resolve();
            });
        }

        async function scanForm() {
            showModal.value = false;
            beingScanned.value = true;
            try {
                const response = await postImage(imageStore.storedFile);
                checkboxCoords.value = response.checkbox;
                inputFieldCoords.value = response.inputLine;
                beingScanned.value = false;
                error.value = '';
            } catch (e: any) {
                error.value = e.message;
                beingScanned.value = false;
                return;
            }
            showModal.value = true;
            await nextTick();
            if (scannedImage.value) {
                const { width } = scannedImage.value.getBoundingClientRect();
                domToActualRatio.value = width / resolution.width;
                checkboxCoords.value = checkboxCoords.value?.map((coords) => {
                    return coords.map((coords) => (coords * (domToActualRatio.value ?? 0) - 2.5));
                })
                inputFieldCoords.value = inputFieldCoords.value?.map((coords) => {
                    return coords.map((coords) => (coords * (domToActualRatio.value ?? 0)));
                })
            }
            beingScanned.value = false;
        }

        function download() {
            const doc = new jsPDF();
            if (!form.value) return;
            doc.html(form.value, {
                html2canvas: {
                    scale: domToActualRatio.value,
                    logging: true,
                    scrollX: 0,
                    scrollY: 0,
                    windowWidth: resolution.width,
                    windowHeight: resolution.height,
                },
                callback: function (doc) {
                    doc.save();
                }
            });
        }

</script>

<template>
    <main class="flex flex-col items-center transition-all relative h-5/6">
        <DragAndDrop @drop.stop.prevent="handleUpload"
                     @change="handleUpload" />
        <PreviewHeader v-if="imageStore.uploadedImage"
                       :being-scanned="beingScanned"
                       @scanform="scanForm"
                       @change.stop="handleUpload" />

        <div class="relative">
            <div v-if="beingScanned"
                 class="absolute flex items-center inset-0 bg-zinc-600/50 rounded-lg backdrop-blur-[1px]">
                <UploadLoader />
            </div>
            <div v-if="error && !beingScanned"
                 class="absolute flex flex-col justify-center items-center inset-0 bg-zinc-600/50 rounded-lg backdrop-blur-[1px]">
                <i class="bi bi-exclamation-triangle text-3xl"></i>
                <p>Error: {{ error }}</p>
            </div>
            <img v-if="imageStore.uploadedImage"
                 class="max-h-[50svh] rounded-lg object-contain"
                 :src="imageStore.uploadedImage" />
        </div>
        <p v-if="imageStore.uploadedImage"
           class="ms-2">{{ fileName }}
            <button @click="imageStore.removeImage">
                <i class="text-red-500 bi bi-x-lg"></i>
            </button>
        </p>

        <ModalComponent @close="showModal = false;"
                        :isVisible="showModal">
            <template #header>
                {{ fileName }}
            </template>
            <div class="relative"
                 ref="form">
                <input v-for="(coords, index) in checkboxCoords"
                       :key="index"
                       type="checkbox"
                       class="absolute appearance-none"
                       :style="`left: ${coords[0]}px; top: ${coords[1]}px;`">
                <input v-for="(coords, index) in inputFieldCoords"
                       :key="index"
                       type="text"
                       class="absolute bg-transparent text-black text-xs"
                       :style="`left: ${coords[0]}px; top: calc(${coords[1]}px - 18px); width: ${coords[2] - coords[0]}px`"
                       style="font-family: Arial">
                <div class="max-h-[90svh] overflow-scroll">
                    <img v-if="imageStore.uploadedImage"
                         class="rounded-sm"
                         :src="imageStore.uploadedImage"
                         ref="scannedImage" />
                </div>
            </div>
            <template #footer>
                <button @click="download"
                        class="transition-colors bg-green-600 hover:bg-green-900 rounded-md mx-auto mt-2 size-10">
                    <i class="bi bi-download text-2xl"></i>
                </button>
            </template>
        </ModalComponent>
    </main>
</template>

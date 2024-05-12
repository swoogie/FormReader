<script setup
        lang="ts">
        import WelcomeItem from '@/components/WelcomeItem.vue';
</script>

<template>
  <main>
    <WelcomeItem>
      <template #icon>
        <i class="bi bi-file-earmark-text "></i>
      </template>
      <template #heading>Provide form</template>
        <RouterLink class="text-green-400"
                    to="/upload">Upload</RouterLink> or take a picture of your form
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <i class="bi bi-eye"></i>
      </template>
      <template #heading>Preview</template>
      Preview the form you uploaded to ensure it is correct
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <i class="bi bi-file-earmark-break"></i>
      </template>
      <template #heading>Scan</template>
      Click 'Scan' to scan and extract the input fields from your form
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <i class="bi bi-input-cursor-text"></i>
      </template>
      <template #heading>Input</template>
      Fill in the extracted fields with the correct information
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <i class="bi bi-download"></i>
      </template>
      <template #heading>Save</template>
      Click 'Save' to download the filled form
    </WelcomeItem>
  </main>
</template>

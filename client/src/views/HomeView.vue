<script setup
        lang="ts">
        import WelcomeItem from '@/components/WelcomeItem.vue';
</script>

<template>
  <main>
    <WelcomeItem>
      <template #icon>
        <i class="bi bi-file-earmark-text text-2xl"></i>
      </template>
      <template #heading>Provide form</template>
      Upload or take a picture of your form
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <i class="bi bi-eye text-2xl"></i>
      </template>
      <template #heading>Preview</template>
      Preview the form you uploaded to ensure it is correct
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <i class="bi bi-file-earmark-break text-2xl"></i>
      </template>
      <template #heading>Scan</template>
      Click 'Scan' to scan and extract the input fields from your form
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <i class="bi bi-input-cursor-text text-2xl"></i>
      </template>
      <template #heading>Input</template>
      Fill in the extracted fields with the correct information
    </WelcomeItem>

    <WelcomeItem>
      <template #icon>
        <i class="bi bi-download text-2xl"></i>
      </template>
      <template #heading>Save</template>
      Click 'Save' to download the filled form
    </WelcomeItem>
  </main>
</template>

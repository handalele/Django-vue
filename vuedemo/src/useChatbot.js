// useChatbot.js
import {ref} from 'vue';

export function useChatbot(token, baseUrl) {
    const isLoaded = ref(false);

    function loadScript() {
        const script = document.createElement('script');
        script.src = `${baseUrl}/embed.min.js?token=${token}`;
        script.defer = true;
        script.onload = () => {
            isLoaded.value = true;
            console.log('Chatbot script loaded');
        };
        document.head.appendChild(script);
    }

    return {isLoaded, loadScript};
}
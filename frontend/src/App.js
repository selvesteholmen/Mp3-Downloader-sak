import { useState } from "react";
import { Provider } from "./components/ui/provider";
import { Button, Box, Input, Flex, Text } from "@chakra-ui/react";
import { ToggleTip } from "./components/ui/toggle-tip";
import { LuInfo } from "react-icons/lu";
import axios from "axios";
import { Toaster, toaster } from "./components/ui/toaster";
import validator from "validator";

const api = axios.create({ baseURL: "http://localhost:8000" });

function App() {
  const [isYoutube, setIsYoutube] = useState(null);
  const [inputValue, setInputValue] = useState("");
  const [isDownloading, setIsDownloading] = useState(false);

  const handleDownload = async () => {
    if (!inputValue.trim()) {
      toaster.create({ title: "Error", description: "No Input" });
      return;
    }

    if (isYoutube === null) {
      console.error("Please select a platform.");
      toaster.create({ title: "Error", description: "Please select a platform before downloading." });
      return;
    }

    if (isYoutube && !validator.isURL(inputValue, { protocols: ['https'], require_protocol: true })) {
      toaster.create({ title: "Error", description: "The YouTube link must start with 'https://' and be a valid URL." });
      return;
    }

    if (!isYoutube && /^https:\/\/(www\.)?youtube\.com\/.+/.test(inputValue)) {
      toaster.create({ title: "Oops", description: "You typed a YouTube link. Remember to switch to YouTube for YouTube links." });
      return;
    }

    const payload = isYoutube ? { link: inputValue } : { search: inputValue };
    const endpoint = isYoutube ? "/youtube_download" : "/spotify_download";

    const loadingToast = toaster.create({ title: "Download Started", description: "Please wait while the file downloads", type: "loading" });

    try {
      setIsDownloading(true);
      const response = await api.post(endpoint, payload);
      console.log("Download started", response.data);
      toaster.dismiss(loadingToast);
      toaster.create({ title: "Success", description: "File downloaded successfully, see downloads folder." });
    } catch (error) {
      console.error("Download error:", error);
      toaster.dismiss(loadingToast);
      toaster.create({ title: "Error", description: "Failed to start download." });
    } finally {
      setIsDownloading(false);
    }
  };

  return (
    <Provider>
      <Toaster />
      <Box
        height="100vh"
        background="linear-gradient(to bottom, orange 10%, red 100%)"
        display="flex"
        flexDirection="column"
        alignItems="center"
        justifyContent="center"
        textAlign="center"
      >
        <Text fontSize="5xl" fontWeight="bold" color="white" mb={2}>
          Holmen MP3 Downloader
        </Text>
        <Text fontSize="md" color="white" mb={4}>
          For those who hate the sketchy website converters
        </Text>

        <Input
          bg="white"
          color="black"
          placeholder={isYoutube === null ? " " : isYoutube ? "Insert YouTube link" : "Insert song title & artist"}
          width="300px"
          mb={4}
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
        />

        <Flex mb={4} gap={2}>
          <Button
            onClick={() => setIsYoutube(true)}
            colorScheme={isYoutube ? "blue" : "gray"}
            border={isYoutube ? "2px solid black" : "none"}
          >
            YouTube
          </Button>
          <Button
            onClick={() => setIsYoutube(false)}
            colorScheme={!isYoutube && isYoutube !== null ? "green" : "gray"}
            border={!isYoutube && isYoutube !== null ? "2px solid black" : "none"}
          >
            Spotify
          </Button>
        </Flex>

        <Button mb={4} onClick={handleDownload} disabled={isDownloading}>
          Download
        </Button>

        <ToggleTip content={
          <>
            <p>Select a platform using the buttons.</p>
            <p>For Spotify, type the song title and artist name.</p>
            <p>For YouTube, paste the video link.</p>
          </>
        }>
          <Button size="xs" variant="unstyled" color="white">
            <LuInfo />
          </Button>
        </ToggleTip>
      </Box>
    </Provider>
  );
}

export default App;

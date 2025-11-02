import os
import glob
import random
import sys
import pygame
import whisper

def main():
    extensions = ['.mp4', '.mp3', '.wav', '.m4a']
    files = []
    for ext in extensions:
        files += glob.glob('*' + ext)

    transcribed = 0
    model = whisper.load_model("base")

    for file in files:
        txt = file + '.txt'
        if os.path.exists(txt):
            continue

        result = model.transcribe(file)
        with open(txt, 'w') as f:
            for segment in result['segments']:
                start = segment['start']
                end = segment['end']
                text = segment['text']
                f.write(f"[{start:.1f}s - {end:.1f}s] {text}\n")

        transcribed += 1

    if transcribed == 0:
        # No transcription needed, play random chiptune with GUI for input handling
        myth_files = glob.glob('myth/*')
        if not myth_files:
            # Can't show error without console, so just exit
            return

        pygame.init()
        screen = pygame.display.set_mode((500, 100))
        pygame.display.set_caption("Stenografen Music Player")
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 24)

        selected = None
        while selected is None:
            selected = random.choice(myth_files)
            base = os.path.basename(selected)
            if base == 'myth.sid':
                # Warn and confirm
                warn_text = "Warning: myth.sid selected. Press Y to play, N to skip."
                confirmed = False
                while not confirmed:
                    screen.fill((0, 0, 0))
                    text_surf = font.render(warn_text, True, (255, 255, 255))
                    screen.blit(text_surf, (10, 30))
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_y:
                                confirmed = True
                                break
                            elif event.key == pygame.K_n:
                                selected = None
                                confirmed = True
                                break

                    clock.tick(30)

            if selected is None:
                continue

            # Attempt to play
            try:
                pygame.mixer.music.load(selected)
                pygame.mixer.music.play(-1)  # Loop
                play_text = f"Playing {base}. Press M to mute."
                break  # Success, exit selection loop
            except pygame.error as e:
                error_text = f"Error loading {base}: {str(e)}. Press any key to continue."
                waiting = True
                while waiting:
                    screen.fill((0, 0, 0))
                    text_surf = font.render(error_text, True, (255, 0, 0))
                    screen.blit(text_surf, (10, 10))
                    pygame.display.flip()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.KEYDOWN:
                            waiting = False

                    clock.tick(30)
                selected = None  # Repick

        # Playback loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_m:
                        pygame.mixer.music.stop()
                        running = False

            screen.fill((0, 0, 0))
            text_surf = font.render(play_text, True, (255, 255, 255))
            screen.blit(text_surf, (10, 30))
            pygame.display.flip()
            clock.tick(30)

        pygame.quit()

if __name__ == '__main__':
    main()

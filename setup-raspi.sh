#!/bin/bash
# Raspberry Pi Setup Script for Voice Client

echo "Setting up Raspberry Pi for Voice Client..."

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install audio dependencies
echo "Installing audio dependencies..."
sudo apt-get install -y portaudio19-dev python3-pyaudio alsa-utils

# Install Python dependencies
echo "Installing Python packages..."
pip3 install -r requirements.txt

# Test audio devices
echo "Testing audio devices..."
echo "Available recording devices:"
arecord -l
echo ""
echo "Available playback devices:"
aplay -l

# Create ALSA configuration if needed
echo "Creating ALSA configuration..."
cat > ~/.asoundrc << EOF
pcm.!default {
    type asym
    playback.pcm {
        type plug
        slave.pcm "hw:0,0"
    }
    capture.pcm {
        type plug
        slave.pcm "hw:1,0"
    }
}
EOF

echo "Setup complete! You may need to adjust the device numbers in ~/.asoundrc"
echo "based on your audio hardware configuration."
#!/bin/bash
# Raspberry Pi Setup Script for Voice Client

echo "Setting up Raspberry Pi for Voice Client..."

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install audio dependencies
echo "Installing audio dependencies..."
sudo apt-get install -y portaudio19-dev libportaudio2 libportaudiocpp0 python3-pyaudio alsa-utils

# Fix PortAudio library linking issues
echo "Fixing PortAudio library issues..."
sudo ldconfig

# Create symbolic link if needed
if [ ! -f /usr/lib/$(uname -m)-linux-gnu/libportaudio.so.2 ]; then
    echo "Creating PortAudio symbolic link..."
    sudo ln -sf /usr/lib/$(uname -m)-linux-gnu/libportaudio.so /usr/lib/$(uname -m)-linux-gnu/libportaudio.so.2
fi

# Install Python dependencies
echo "Installing Python packages..."
# Use system package for pyaudio to avoid compilation issues
sudo apt-get install -y python3-pyaudio
# Install other requirements
pip3 install -r requirements.txt --no-deps pyaudio

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
echo ""
echo "If you still get PortAudio errors, try:"
echo "  1. sudo apt-get install --reinstall libportaudio2"
echo "  2. export LD_LIBRARY_PATH=/usr/lib/$(uname -m)-linux-gnu:$LD_LIBRARY_PATH"
echo "  3. Reboot your Raspberry Pi"
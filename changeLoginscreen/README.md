# ubuntu-gdm-set-background script (for changing Ubuntu 20.04, 21.04 & 21.10 GDM Background) HELP

Download the script with below command


````
wget -qO - https://github.com/PRATAP-KUMAR/ubuntu-gdm-set-background/archive/main.tar.gz | tar zx --strip-components=1 ubuntu-gdm-set-background-main/ubuntu-gdm-set-background
````

there are four options
1. background with image
2. background with color
3. background with gradient horizontal ( requires two valid hex color inputs)
4. background with gradient vertical ( requires two valid hex color inputs)

tip: be ready with valid hex color code in place of below example like #aAbBcC or #dDeEfF. Change them to your preffered hex color codes.
you may choose colors from https://www.color-hex.com/

Example Commands:

1. `sudo ./ubuntu-gdm-set-background --image /home/user/backgrounds/image.jpg`
2. `sudo ./ubuntu-gdm-set-background --color \#aAbBcC`
3. `sudo ./ubuntu-gdm-set-background --gradient horizontal \#aAbBcC \#dDeEfF`
4. `sudo ./ubuntu-gdm-set-background --gradient vertical \#aAbBcC \#dDeEfF`
5. `sudo ./ubuntu-gdm-set-background --reset`
6. `./ubuntu-gdm-set-background --help`

RESCUE_MODE, Example Commands:

1. `sudo ./ubuntu-gdm-set-background --image /home/user/backgrounds/image.jpg rescue`
2. `sudo ./ubuntu-gdm-set-background --color \#aAbBcC rescue`
3. `sudo ./ubuntu-gdm-set-background --gradient horizontal \#aAbBcC \#dDeEfF rescue`
4. `sudo ./ubuntu-gdm-set-background --gradient vertical \#aAbBcC \#dDeEfF rescue`

Why RESCUE_MODE?
It is when you try to change the background with some other scripts and then interacted with this script,
there will be some conflicts. In case you ran other scripts to change the background and then tried this script,
found conflicts? then add 'rescue' to the end of the command as mentiond above.

Please note that for 'RESCUE_MODE' active internet connection is necessary

![1](https://user-images.githubusercontent.com/40719899/138041931-c61f5223-b446-47f4-bc30-4926b380db9f.png)

![2](https://user-images.githubusercontent.com/40719899/138041947-ca1d8f27-a294-45c4-9f0a-50e6c5de8004.png)

![3](https://user-images.githubusercontent.com/40719899/138041955-321aa1bb-1d1f-4b61-96ff-9accc129b846.png)

![4](https://user-images.githubusercontent.com/40719899/138041957-e8dcae5c-b52d-4c58-be04-d899b9e49ce8.png)

![5](https://user-images.githubusercontent.com/40719899/138041959-32db8c1b-7679-4513-9c15-5071f231f796.png)

![6](https://user-images.githubusercontent.com/40719899/138041960-3978f9c0-8cee-4a68-82fb-5f77865c8c77.png)

![7](https://user-images.githubusercontent.com/40719899/138041961-7c58337d-9cbb-42d4-974f-d260a024e5fd.png)

![8](https://user-images.githubusercontent.com/40719899/138041963-a4981163-1c1f-4886-9a67-cfc1827a5d80.png)

![9](https://user-images.githubusercontent.com/40719899/138041965-19699e82-4d31-4539-80ac-3f3bc559504d.png)

![10](https://user-images.githubusercontent.com/40719899/138041973-bde88f7c-8fe5-4862-87bc-3affd4d44dbf.png)

![11](https://user-images.githubusercontent.com/40719899/138041974-e229d7a4-9950-4eec-b837-716d7947b192.png)

![12](https://user-images.githubusercontent.com/40719899/138041976-8c6f1f36-a32c-4ed3-993d-22fe66a9fc42.png)


# APthief

## What
This is a demonstration of a 3DS flaw that allows one to extract an APcert from a 00000000.ctx file, which are temporarily created when a title is downloaded. No userland 3DS code execution is necessary.

## How
When a user "Purchases" a title (free or paid) from the eshop, the 00000000.ctx is immediately created on the sdmc card. This file is, under the cloak of aes-ctr crypto, initialized to all FFs. Once the user actually initiates the download, an APcert is created inside the .ctx file and remains there until the download is completed or cancelled, then the .ctx file is deleted. If a user makes a seperate copy of the .ctx before and after the download commences, they can create a xorpad to decrypt the APcert. This is a known-plaintext attack. The included .py script will perform this method. As this is just a demo and not production ready code, no instructions will be given (read the source if curious). This method has no current guarantee of being added to seedminer officially, if at all.

## Why
Within the APcert is the 3ds console's deviceID. The deviceID is mathematically related to the console's LFCS, which can greatly aid in the normally long brutefore necessary to extract the LFCS from the "MiiQR" variant of Seedminer.

## Where
The .ctx file will be created inside the title's folder on the sd card (hint: select download later after Purchase, then turn off console and look at sd card)<br>
sdmc:/Nintendo 3DS/ID0/ID1/title/0004000X/XXXXXXXX/00000000.ctx<br>
An easy way to find it is type .ctx into your operating system's search bar, within the sd drive that has your 3ds sd card.

## When
Any time the 3DS eshop is open. Keep in mind that this should work with free cart updates too, which are supposed to be supported past the eshop closure date of March 27, 2023.
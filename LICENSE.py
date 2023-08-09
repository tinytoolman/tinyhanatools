def print_bold(text):
    print('\033[1m' + text + '\033[0m')

def print_license():
    license_text = """
GNU GENERAL PUBLIC LICENSE
Version 3, 29 June 2007

TinyHanaTools

Company: Schoeman and Brink, LLC
Author: Tinus Mario Brink "Tiny"
Website: www.sabtec.co
Date: 2023

Preamble:

This program, TinyHanaTools, is designed to assist in the administration of HANA on Linux. As the author and copyright holder, Tinus Mario Brink "Tiny" grants you certain rights to use, modify, and distribute this software under the terms of the GNU General Public License version 3 or any later version, provided the conditions specified in this license are met.

TERMS AND CONDITIONS:

0. Definitions.

"The Program" refers to TinyHanaTools, including any modifications, additions, or derivatives.

"The License" refers to this GNU General Public License, version 3.

1. Copyright and License.

a. Copyright Holder: Tinus Mario Brink "Tiny".
b. Company: Schoeman and Brink, LLC.

You are granted a worldwide, royalty-free, non-exclusive license to use, copy, modify, and distribute the Program in both source code and compiled forms, along with any associated documentation.

2. Restrictions.

a. You may not use the name "TinyHanaTools" or any variation that may cause confusion without explicit permission from Tinus Mario Brink "Tiny" and Schoeman and Brink, LLC.

b. You may not sublicense, sell, lease, rent, or otherwise commercialize the Program or any part thereof, unless explicit written permission is granted by Tinus Mario Brink "Tiny" and Schoeman and Brink, LLC.

c. Please notify Tinus Mario Brink "Tiny" and Schoeman and Brink, LLC at admin@sabtec.co of any programs you have made derived from the original code so they could publish your open work links as well.

3. Share-Alike Requirement.

If you modify the Program or create derivative works based on it, you must distribute such modifications or derivatives under the same terms and conditions as this License. This requirement applies to all subsequent recipients of your modified or derivative work.

4. Warranty Disclaimer.

The Program is provided "as is," without any warranty of any kind, either expressed or implied. Tinus Mario Brink "Tiny" and Schoeman and Brink, LLC disclaim all warranties, including but not limited to the implied warranties of merchantability and fitness for a particular purpose. You assume all risks and responsibilities for using the Program.

5. Limitation of Liability.

In no event shall Tinus Mario Brink "Tiny" or Schoeman and Brink, LLC be liable for any damages, including but not limited to direct, indirect, special, exemplary, incidental, or consequential damages arising out of or in connection with the use or performance of the Program.

6. Governing Law.

This License shall be governed by the laws of [Your Jurisdiction], excluding its conflict-of-law provisions.

END OF TERMS AND CONDITIONS

For more details, please refer to the full text of the GPLv3 license available at https://www.gnu.org/licenses/gpl-3.0.en.html.
    """

    print(license_text)

def main():
    while True:
        print_license()
        print_bold("0.  Back")
        choice = input("Enter your choice: ")
        if choice == '0':
            break

if __name__ == '__main__':
    main()

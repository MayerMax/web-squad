_OFFSETS = {
    '0': 0,
    '1': -35,
    '2': -70,
    '3': -105,
    '4': -140,
    '5': -175,
    '6': -209,
    '7': -238,
    '8': -275,
    '9': -310
}

MARGIN = 35


def convert_counter_in_html(number):
    """
    :param number: as string
    :return: html with resource image as background and offsets, styles already included in landing.html
    """
    if len(number) < 3:
        number = '0{}'.format(number)
    html_block = []

    if len(number) < 2:
        number = '00{}'.format(number)

    for idx, digit in enumerate(number):
        if digit == '0' and idx == 0:
                margin = 0
        else:
            margin = MARGIN * idx

        html_block.append("<li class='digits' style='{}'></li>".format(
            'background: url("../resources/rsz_digits.png") {}px 0; left: {}px;'.format(_OFFSETS[digit], margin)
        ))
    return """
        <div style="position: relative;">
            <ul>
            {}
            </ul>
        </div>
    """.format('\r\n'.join(html_block))

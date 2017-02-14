# amavisOTX
An Amavis plugin for checking known bad file hashes from Open Threat Exchange.

Add it to Amavis in the @av_scanners array:

    ['AmavisOTX',
      '/usr/local/bin/AmavisOTX',
      '{}',
      qr/^OK/m,
      qr/^Found hash from (https:\/\/.*) in (?:.*)$/m,
    ],


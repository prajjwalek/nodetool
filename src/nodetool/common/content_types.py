CONTENT_TYPE_TO_EXTENSION = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "image/gif": "gif",
    "image/svg+xml": "svg",
    "image/webp": "webp",
    "image/tiff": "tiff",
    "image/bmp": "bmp",
    "text/plain": "txt",
    "text/csv": "csv",
    "text/html": "html",
    "text/css": "css",
    "text/javascript": "js",
    "text/xml": "xml",
    "application/json": "json",
    "application/pdf": "pdf",
    "application/zip": "zip",
    "application/x-7z-compressed": "7z",
    "application/x-rar-compressed": "rar",
    "application/x-tar": "tar",
    "application/x-bzip": "bz",
    "application/x-bzip2": "bz2",
    "application/x-xz": "xz",
    "application/x-lzip": "lz",
    "application/x-lzma": "lzma",
    "application/x-compress": "Z",
    "application/x-gzip": "gz",
    "audio/midi": "midi",
    "audio/mpeg": "mp3",
    "audio/mp3": "mp3",
    "audio/webm": "webm",
    "audio/ogg": "ogg",
    "audio/wav": "wav",
    "audio/aac": "aac",
    "audio/wave": "wave",
    "audio/x-wav": "wav",
    "audio/x-aiff": "aiff",
    "audio/x-flac": "flac",
    "audio/x-m4a": "m4a",
    "video/mpeg": "mpeg",
    "video/mp4": "mp4",
    "video/webm": "webm",
    "video/ogg": "ogg",
    "video/quicktime": "mov",
    "video/x-msvideo": "avi",
    "video/x-flv": "flv",
    "video/x-m4v": "m4v",
    "video/3gpp": "3gp",
    "video/3gpp2": "3g2",
}

EXTENSION_TO_CONTENT_TYPE = {
    value: key for key, value in CONTENT_TYPE_TO_EXTENSION.items()
}

from storages.backends.s3boto import S3BotoStorage

class FixedS3BotoStorage(S3BotoStorage):
    def url(self, name):
        """
        Change URL's generated in the following format: http(s)://bucket.name.s3.amazonaws.com/.../
        Into the format: http(s)://s3.amazonaws.com/bucket.name/.../
        """

        url = super(FixedS3BotoStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url
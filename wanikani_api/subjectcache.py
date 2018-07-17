class SubjectCache:
    class __SubjectCache:
        def __init__(self, subjects):

            self._populate_cache(subjects)

        def get(self, subject_id):
            try:
                return self.cached_subjects[subject_id]
            except KeyError:
                raise KeyError(
                    "We couldn't find a subject with ID {} in the cache!".format(
                        subject_id
                    )
                )

        def _populate_cache(self, subjects):
            self.cached_subjects = {subject.id: subject for subject in subjects}

    instance = None

    def __init__(self, subjects):
        if not SubjectCache.instance:
            SubjectCache.instance = SubjectCache.__SubjectCache(subjects)

    def __getattr__(self, name):
        return getattr(self.instance, name)

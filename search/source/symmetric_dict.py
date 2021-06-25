class SymmetricDict(dict):

    def __setitem__(self, k, v) -> None:
        if k in self:
            del self[k]
        if v in self:
            del self[v]
        dict.__setitem__(self, k, v)
        dict.__setitem__(self, v, k)

    def __delitem__(self, v) -> None:
        dict.__delitem__(self, self[v])
        dict.__delitem__(self, v)

    def __len__(self):
        return dict.__len__(self) // 2

    

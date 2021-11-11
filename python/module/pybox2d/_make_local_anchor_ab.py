from .extend_math import vec2

def _make_local_anchor_ab(body_a, body_b, 
        local_anchor_a=None, local_anchor_b=None, local_anchor=None,
        anchor_a=None, anchor_b=None, anchor=None):
    def make_anchor(mine_anchor=None, shared_anchor=None):
        if mine_anchor is None and shared_anchor is not None:
            return shared_anchor
        elif mine_anchor is not None and shared_anchor is None:
            return mine_anchor
        elif  mine_anchor is  None and shared_anchor is None:
            return None
        else:
            raise RuntimeError("ambigious anchor specification")
    def make_local_anchor(body, local_anchor=None, anchor=None):
        if local_anchor is None :
            if anchor is not None:
                local_anchor = body.get_local_point(vec2(anchor))
            else:
                local_anchor = vec2(0,0) 
        else :
            assert anchor is None, "either local_anchor or anchor must be None"

        return  vec2(local_anchor)
    anchor_a = make_anchor(mine_anchor=anchor_a, shared_anchor=anchor)
    anchor_b = make_anchor(mine_anchor=anchor_b, shared_anchor=anchor)
    local_anchor_a = make_anchor(mine_anchor=local_anchor_a, shared_anchor=local_anchor)
    local_anchor_b = make_anchor(mine_anchor=local_anchor_b, shared_anchor=local_anchor)

    local_anchor_a = make_local_anchor(body_a, local_anchor_a, anchor_a)
    local_anchor_b = make_local_anchor(body_b, local_anchor_b, anchor_b)


    return local_anchor_a, local_anchor_b
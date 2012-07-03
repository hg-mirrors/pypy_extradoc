

    def specialize_more_blocks(self):
        while True:
            # look for blocks not specialized yet
            pending = [block for block in self.annotator.annotated
                             if block not in self.already_seen]
            if not pending:
                break

            # specialize all blocks in the 'pending' list
            for block in pending:
                self.specialize_block(block)
                self.already_seen.add(block)




    def specialize_more_blocks(self):
        while True:
            # look for blocks not specialized yet
            pending = [block for block in self.annotator.annotated
                             if block not in self.already_seen]
            if not pending:
                break

            # specialize all blocks in the 'pending' list
            # *using transactions*
            for block in pending:
                transaction.add(self.specialize_block, block)
            transaction.run()

            self.already_seen.update(pending)
